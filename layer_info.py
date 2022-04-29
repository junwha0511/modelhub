positional_params_INFO = {
    "Conv2D": { # https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D
        "n_positional": 2, 
        "positional_params_names": ["filters", "kernel_size"],
        "positional_params_types": ["int", "tuple-2"],
        "keyword_params_map": {
            "strides": "tuple-2",
            "padding": "string",
            "input_shape": "tuple-n",
            "...": "More parameters exist, but this is hackathon:)"
        },
    },
    "MaxPool2D": { # https://www.tensorflow.org/api_docs/python/tf/keras/layers/MaxPool2D
        "n_positional": 0,
        "positional_params_names": [],
        "positional_params_types": [],
        "keyword_params_map": {
            "pool_size": "int|tuple-2",
            "strides": "tuple-2|tuple-2",
            "padding": "string",
            "input_shape": "tuple-n",
            "...": "More parameters exist, but this is hackathon:)",
        }
    },
    "MaxPooling2D": {
        "n_positional": 1,
        "positional_params_names": ["pool_size"],
        "positional_params_types": ["int"],
        "keyword_params_map": {
            "...": "More parameters exist, but this is hackathon:)",
        }
    },
    "Flatten": { # https://www.tensorflow.org/api_docs/python/tf/keras/layers/Flatten
        "n_positional": 0,
        "positional_params_names": [],
        "positional_params_types": [],
        "keyword_params_map": {
            "input_shape": "tuple-n",
        },
    },
    "Dense": { # https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dense
        "n_positional": 1,
        "positional_params_names": ["units"],
        "positional_params_types": ["int"],
        "keyword_params_map": {
            "activation": "string",
            "use_bias": "boolean",
            "input_shape": "tuple-n",
            "...": "More parameters exist, but this is hackathon:)",
        },
    },
    "Dropout": { # https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dropout
        "n_positional": 1,
        "positional_params_names": ["rate"],
        "positional_params_types": ["float"],
        "keyword_params_map": {
            "input_shape": "tuple-n",
            "...": "More parameters exist, but this is hackathon:)",
        },
    },
    "BatchNormalization": { # https://www.tensorflow.org/api_docs/python/tf/keras/layers/BatchNormalization
        "n_positional": 0,
        "positional_params_names": [],
        "positional_params_types": [],
        "keyword_params_map": {
            "input_shape": "tuple-n",
            "...": "More parameters exist, but this is hackathon:)",
        },
    },
}