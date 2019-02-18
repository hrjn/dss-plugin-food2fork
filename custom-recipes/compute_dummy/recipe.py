
import dataiku
from dataiku.customrecipe import *

output_names = get_output_names_for_role('output_role')
output_datasets = [dataiku.Dataset(name) for name in output_names]

my_variable = get_recipe_config()['parameter_name']

# For optional parameters, you should provide a default value in case the parameter is not present:
my_variable = get_recipe_config().get('parameter_name', None)

# Note about typing:
# The configuration of the recipe is passed through a JSON object
# As such, INT parameters of the recipe are received in the get_recipe_config() dict as a Python float.
# If you absolutely require a Python int, use int(get_recipe_config()["my_int_param"])


#############################
# Your original recipe
#############################

# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu



# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

dummy_df = ... # Compute a Pandas dataframe to write into dummy


# Write recipe outputs
dummy = dataiku.Dataset("dummy")
dummy.write_with_schema(dummy_df)
