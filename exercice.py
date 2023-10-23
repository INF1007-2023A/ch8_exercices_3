#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import struct
import math
from collections import namedtuple


SAMPLING_FREQ = 44100 # Hertz, taux d'échantillonnage standard des CD
SAMPLE_BITS = 16
SAMPLE_WIDTH = SAMPLE_BITS // 8
MAX_SAMPLE_VALUE = 2**(SAMPLE_BITS-1) - 1

# Les formats d'encodage (struct) pour les sous-entêtes.
RIFF_HEADER_STRUCT = "4sI 4s"
FORMAT_HEADER_STRUCT = "4sI HHIIHH"
DATA_HEADER_STRUCT = "4sI"
# Le format d'encodage pour les entêtes.
WAVE_FILE_HEADERS_STRUCT = "<" + RIFF_HEADER_STRUCT + FORMAT_HEADER_STRUCT + DATA_HEADER_STRUCT


# Contient tous les champs des entêtes d'un fichier WAVE.
WaveFileHeaders = namedtuple("WaveFileHeaders", """
	riff_id,
	file_size,
	wave,
	fmt_id,
	fmt_size,
	wav_type,
	num_channels,
	sampling_freq,
	bytes_per_second,
	bytes_per_sample,
	sample_bits,
	data_id,
	data_size
""")


def merge_channels(channels):
	# À partir de plusieurs listes d'échantillons (réels), les combiner de façon à ce que la liste retournée aie la forme :
	# [c[0][0], c[1][0], c[2][0], c[0][1], c[1][1], c[2][1], ...] où c est l'agument channels
	pass

def separate_channels(samples, num_channels):
	# Faire l'inverse de la fonction merge_channels
	# Si on a en entrée [11, 21, 12, 22, 13, 23]
	# Sur deux channels on obtiendrait :
	# [
	#   [11, 12, 13]
	#   [21, 22, 23]
	# ]
	pass

def sine_gen(freq, amplitude, duration_seconds):
	# Générer une onde sinusoïdale à partir de la fréquence et de l'amplitude donnée, sur le temps demandé et considérant le taux d'échantillonnage.
	# Les échantillons sont des nombres réels entre -1 et 1.
	# Formule de la valeur y d'une onde sinusoïdale à l'angle x en fonction de sa fréquence F et de son amplitude A :
	# y = A * sin(F * x), où x est en radian.
	# Si on veut le x qui correspond au moment t, on peut dire que 2π représente une seconde, donc x = t * 2π.
	# Or t est en secondes, donc t = i / nb_échantillons_par_secondes, où i est le numéro d'échantillon.
	pass

def create_headers(num_samples):
	headers_size = struct.calcsize(WAVE_FILE_HEADERS_STRUCT)
	data_size = num_samples * SAMPLE_WIDTH
	riff_file_size = struct.calcsize(WAVE_FILE_HEADERS_STRUCT) - 8 + data_size

	return WaveFileHeaders(
		riff_id=          b"RIFF",
		file_size=        riff_file_size,
		wave=             b"WAVE",
		fmt_id=           b"fmt ",
		fmt_size=         struct.calcsize(FORMAT_HEADER_STRUCT) - 8,
		wav_type=         1,
		num_channels=     2,
		sampling_freq=    SAMPLING_FREQ,
		bytes_per_second= SAMPLING_FREQ * SAMPLE_WIDTH,
		bytes_per_sample= SAMPLE_WIDTH,
		sample_bits=      SAMPLE_BITS,
		data_id=          b"data",
		data_size=        data_size
	)

def convert_to_bytes(samples):
	# Convertir les échantillons en tableau de bytes en les convertissant en entiers 16 bits.
	# Les échantillons en entrée sont entre -1 et 1, nous voulons les mettre entre -MAX_SAMPLE_VALUE et MAX_SAMPLE_VALUE
	pass

def encode_wave_data(samples):
	# Créer les entêtes à encoder à l'aide de create_headers, les encoder en octets avec le format d'encodage donné dans la constante WAVE_FILE_HEADERS_STRUCT.
	# Convertir les échantillons en octets avec la fonction convert_to_bytes.
	# Retourner les octets d'entête et les octets de données (en deux valeurs).
	pass

def convert_to_samples(sample_bytes):
	# Faire l'opération inverse de convert_to_bytes, en convertissant des échantillons entiers signés de 16 bits en échantillons réels.
	pass

def decode_wave_data(file_bytes):
	# Décoder les entês en octets avec le format d'encodage donné dans la constante WAVE_FILE_HEADERS_STRUCT.
	# Décoder les octets de données en échantillons réel avec la fonction convert_to_samples en se positionnant au début des données (après les octets).
	# Retourner les entêtes décodés (sous la forme d'un WaveFileHeaders) et la liste d'échantillons réel en deux valeurs.
	pass


def main():
	if not os.path.exists("output"):
		os.mkdir("output")

	# Si on veut juste tester l'encodage des échantillons, on peut appeler convert_to_bytes avec quelques échantillons, écrire les octets directement dans un fichier binaire sans entête et les importer comme «Raw data» dans Audacity.
	with open("output/test.bin", "wb") as out_file:
		data = convert_to_bytes([0.8, -0.8, 0.5, -0.5, 0.2, -0.2])
		out_file.write(data)

	# Exemple simple avec quelques échantillons pour tester le fonctionnement de l'écriture.
	with open("output/test.wav", "wb") as out_file:
		headers, data = encode_wave_data([0.8, -0.8, 0.5, -0.5, 0.2, -0.2])
		out_file.write(headers)
		out_file.write(data)

	with open("output/major_chord.wav", "wb") as out_file:
		# On génére un la3 (220 Hz), un do#4, un mi4 et un la4 (intonnation juste).
		sine_a3 = sine_gen(220, 0.5, 10.0)
		sine_cs4 = sine_gen(220 * (5/4), 0.4, 10.0)
		sine_e4 = sine_gen(220 * (3/2), 0.35, 10.0)
		sine_a4 = sine_gen(220 * 2, 0.3, 10.0)

		# On met les samples dans des channels séparés (la à gauche, mi à droite)
		merged = merge_channels([
			(sum(elems) for elems in zip(sine_a3, sine_cs4)),
			(sum(elems) for elems in zip(sine_e4, sine_a4))
		])
		headers, data = encode_wave_data(merged)

		out_file.write(headers)
		out_file.write(data)

	with open("data/kinship_maj.wav", "rb") as in_file:
		headers, samples = decode_wave_data(in_file.read())
		# On réduit le volume (on pourrait faire n'importe quoi avec les samples à ce stade)
		samples = [s * 0.2 for s in samples]
		headers, data = encode_wave_data(samples)

		with open("output/kinship_mod.wav", "wb") as out_file:
			out_file.write(headers)
			out_file.write(data)

if __name__ == "__main__":
	main()
