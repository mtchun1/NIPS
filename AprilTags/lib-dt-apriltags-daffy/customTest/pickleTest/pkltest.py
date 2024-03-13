import pickle

with open('pose_t.pkl', 'rb') as stream1:
    pose = pickle.load(stream1)

print(pose)

with open('detect.pkl', 'rb') as stream2:
    det = pickle.load(stream2)
print(det)

info = [1,23,3]
pickle.dump([1,2,3], open( "testpickle1.pkl", "wb" ))
pickle.dump(([1,2,3], info), open( "testpickle2.pkl", "wb" ))