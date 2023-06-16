import numpy as np
import openvino.runtime.opset1 as ov
from openvino.runtime import Model, Core

# create a model with MatMul
shape0, shape1 = [2, 5, 3], [2, 3, 5]
param0 = ov.parameter(shape0, name="data0", dtype=np.float32)
param1 = ov.parameter(shape1, name="data1", dtype=np.float32)
matmul = ov.matmul(param0, param1, False, False)
model = Model([matmul.output(0)], [param0, param1], "model")

# infer it on CPU
input_data = { param.any_name : np.random.rand(*param.shape) for param in model.inputs }
core = Core()
compiled_model = core.compile_model(model, "CPU")
output = compiled_model(input_data)

# output
print("result = ", output)
