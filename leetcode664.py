
def strangePrinter(s: str) -> int:
    
    new_s = ""
    for char in s:
        if new_s:
            if char != new_s[-1]:
                new_s += char
        else:
            new_s = char

    char_dict = dict()
    for index, char in enumerate(new_s):
        if char not in char_dict:
            char_dict[char] = [index]
        elif index > char_dict[char][-1]:
            char_dict[char] += [index]
    
    count = 0
    # represents index slice of original string in focus
    s_tuple = (0, len(new_s)-1)
    for index, char in enumerate(new_s):
        if index == 0:
            print("-----------------------")
            print("char: ", char)
            print("tuple before: ", s_tuple)
            print("count before: ", count)
            s_tuple = (1, len(new_s)-1)
            last_of_char = len(new_s)-1
            count += 1
            print("last of char: ", last_of_char)
            print("tuple after: ", s_tuple)
            print("count after: ", count)
        else:
            print("-----------------------")
            print("char: ", char)
            print("tuple before: ", s_tuple)
            print("count before: ", count)
            # Trying to find the last position of current char in this index slice
            print("char dict:" , char_dict[char])
            shared_indexes = list( i for i in char_dict[char] if i in range(s_tuple[0], s_tuple[1]+1))
            if shared_indexes:
                print("shared_indexes:", shared_indexes)
                last_of_char = max(shared_indexes)
            else:
                raise IndexError('no such overlapping values; what do?')
            print("last of char: ", last_of_char)
            count += s_tuple[1] - last_of_char + 1
            if last_of_char is s_tuple[0]:
                break
            s_tuple = (s_tuple[0]+1, last_of_char-1)
            
            print("tuple after: ", s_tuple)
            print("count after: ", count)
    return count


"""
Example: cabacbaa
Iterate along string,
for the given letter (e.g. (index=4, value='c')),
if next letter isn't the same,
    check where the last placement of that letter is,
    create new string that fills in those chars
elif next letter is the same,
    skip letter
elif no next letter,
    break


e.g cbacbacbacba
-----------------
000000000000 - 0
cccccccccccc - 1
ccccccccccbc - 2
ccccccccccba - 3
cbbbbbbbbcba - 4
cbaaaaabbcba - 5
cbaaaaabacba - 6
cbacaaabacba - 7
cbacaacbacba - 8
cbacbacbacba - 9

e.g cbacbacbacba
-----------------
000000000000 - 0
cccccccccccc - 1
ccccccccccbc - 2
ccccccccccba - 3
cbbbbbbbbcba - 4
cbaaaaabbcba - 5
cbaaaaabacba - 6
cbaccccbacba - 7
cbacbccbacba - 8
cbacbacbacba - 9
    

"""

def main():
    print(strangePrinter('aba'))
    

if __name__ == "__main__":
    main()