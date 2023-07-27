# package install
# import subprocess

# for packages in [
#     "tokenizers",
#     "sentencepiece",
#     "focal_loss",
#     "pymysql",
#     "sqlalchemy",
#     "tensorflow",
#     "keras",
#     "scikit-learn",
# ]:
#     subprocess.call(["pip", "install", packages])

# for packages in ["scikit-learn", "keras", "tensorflow", "pickle"]:
#     subprocess.call(["pip", "install", "--upgrade", "--user", packages])


# package import
import pandas as pd
import numpy as np
from tqdm import tqdm, tqdm_notebook

from tokenizers import SentencePieceBPETokenizer
import sentencepiece as spm

import tensorflow as tf
from tensorflow.keras.layers import (
    Input,
    Embedding,
    GRU,
    Dense,
    Dropout,
    BatchNormalization,
    concatenate,
)
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

from keras.models import load_model

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

from focal_loss import SparseCategoricalFocalLoss

import pymysql
from sqlalchemy import create_engine

import re
import joblib
import pickle
import statistics
import warnings
