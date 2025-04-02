import numpy as np
CAVs=np.load("./data/CAVs.npy",allow_pickle=True)
print(np.size(CAVs))




for index in range(20):
    print(CAVs[index].PositionVector[np.where(CAVs[index].PositionVector != 0)[0]])
print(CAVs[0].PositionVector[0:60])