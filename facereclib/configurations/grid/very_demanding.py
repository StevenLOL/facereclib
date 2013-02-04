#!/usr/bin/env python

# setup of the grid parameters

# default queue used for training
training_queue = { 'queue':'q1dm', 'memfree':'64G', 'pe_opt':'pe_mth 8', 'hvmem':'8G', 'io_big':True }

# number of images that one job should preprocess
number_of_images_per_job = 100
preprocessing_queue = {}

# number of features that one job should extract
number_of_features_per_job = 100
extraction_queue = { 'queue':'q1d', 'memfree':'8G', 'io_big':True }

# number of features that one job should project
number_of_projections_per_job = 20
projection_queue = { 'queue':'q1d', 'memfree':'8G', 'io_big':True }

# number of models that should be enrolled by one enroll job
number_of_models_per_enroll_job = 2
enroll_queue = { 'queue':'q1d', 'memfree':'8G', 'io_big':True }

# number of models that one score computation should use
number_of_models_per_score_job = 1
score_queue = { 'queue':'q1d', 'memfree':'8G', 'io_big':True }
