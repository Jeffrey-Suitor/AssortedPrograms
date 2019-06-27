ourSequence = open('originalSequence.txt').read()  # Opens the original sequence
mutationSequence = open('mutationSequence.txt').read()  # Opens the mutation sequence

print("\nOur sequence is " + str(len(ourSequence)) + " long.")  # Prints out the length of our sequence
print("The mutation sequence is " + str(len(mutationSequence)) + ".")  # Prints out the length of the mutation sequence


if len(ourSequence) > len(mutationSequence):  # Deletion mutation
    print("This is a deletion mutation.")
    condition = "missing"

elif len(ourSequence) > len(mutationSequence): # Insertion mutation
    print("This is an insertion mutation.")
    condition = "added" 

else:
    print("This is a missense mutation.")  # Missense mutation
    condition = "replaced"

mutationSequence = mutationSequence + " "

for i in range(len(ourSequence)):
        if ourSequence[i] != mutationSequence[i]:
            print("There is a " + ourSequence[i] + " " + condition + " at position " + str(i) + ".")  # Outputs the results
            break
