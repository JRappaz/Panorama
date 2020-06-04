import pickle
users = []
with open("seeds_ids.txt", "rb") as fp:   # Unpickling
    users = pickle.load(fp)

print(len(users))
users.remove('25073877')
users.remove('44196397')
print(len(users))

with open("seeds_ids_filtered.txt", "wb") as fp:   # Unpickling
    pickle.dump(users, fp)