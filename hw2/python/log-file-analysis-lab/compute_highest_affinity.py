
# No need to process files and manipulate strings - we will
# pass in lists (of equal length) that correspond to 
# sites views. The first list is the site visited, the second is
# the user who visited the site.

# See the test cases for more details.
import operator


def highest_affinity(site_list, user_list, time_list):
  # Returned string pair should be ordered by dictionary order
  # I.e., if the highest affinity pair is "foo" and "bar"
  # return ("bar", "foo").
  result = {}
  su_list = list(zip(site_list, user_list))

  for index, su in enumerate(su_list):
    for i in range(index + 1, len(su_list)):
      su_next = su_list[i]
      if su_next[1] == su[1]:
        key_entry = (su[0], su_next[0])
        if key_entry in result.keys():
          result[key_entry] = result[key_entry] + 1
        else:
          result[key_entry] = 1

  sorted_result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
  return sorted_result[0][0]

if __name__ == '__main__':
  site_list = ["a.com", "b.com", "a.com", "b.com", "a.com", "c.com"]
  user_list = ["andy", "andy", "bob", "bob", "charlie", "charlie"]
  time_list = [1238972321, 1238972456, 1238972618, 1238972899, 1248472489, 1258861829]
  highest_affinity(site_list, user_list, time_list)