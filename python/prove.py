import ezkl
import os
import argparse
from utils import relative_file_path
import json
import torch
from torch.autograd import Variable

parser = argparse.ArgumentParser(
                    prog='Omron AVS ezkl operator engine')

parser.add_argument('-i','--input', nargs='+', help='input data to run on', required=True)

args = parser.parse_args()

input = Variable(torch.Tensor([float(i) for i in args.input]))

data_array = ((input).detach().numpy()).reshape([-1]).tolist()

data_path = relative_file_path("proof/inputs.json")
witness_path = relative_file_path("proof/witness.json")
compiled_model_path = relative_file_path("model_data/network.ezkl")
pk_path = relative_file_path("model_data/test.pk")
vk_path = relative_file_path("model_data/test.vk")
settings_path = relative_file_path("model_data/settings.json")
proof_path =    relative_file_path('proof/proof.json')

# Serialize data into file:
data = dict(input_data = [data_array])
json.dump(data, open(data_path, 'w'))

# Generate the Witness for the proof
ezkl.gen_witness(data_path, compiled_model_path, witness_path)

# Generate the proof
proof = ezkl.prove(
        witness_path,
        compiled_model_path,
        pk_path,
        proof_path,
        "single",
    )
assert ezkl.verify(
        proof_path,
        settings_path,
        vk_path,
    ) == True

onchain_input_array = []

# using a loop
# avoiding printing last comma
formatted_output = "["
for i, value in enumerate(proof["instances"]):
    for j, field_element in enumerate(value):
        onchain_input_array.append(ezkl.felt_to_big_endian(field_element))
        formatted_output += '"' + str(onchain_input_array[-1]) + '"'
        if j != len(value) - 1:
            formatted_output += ", "
    if i != len(proof["instances"]) - 1:
        formatted_output += ", "
formatted_output += "]"

# This will be the values you use onchain
# copy them over to remix and see if they verify
# What happens when you change a value?
print("Inputs: ", formatted_output)
print("Proof: ", proof["proof"])