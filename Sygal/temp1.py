import string 
import random 
import operator

class cl1: 
                   # Class Variable 
  def __init__(self):
    self.name  = ''
    self.name_gen()
              # Instance Variable 
  def name_gen(self,N=8):
    self.name = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
    self.__hash__()

  def __str__(self):
    return self.name
  __repr__ = __str__
  
  def __hash__(self):
    return hash(self.name)

  def __eq__(self, other):
    return (
      self.__class__ == other.__class__ and
      self.name == other.name
    )

class cl2: 
  args = []           # Class Variable 
  def __init__(self,N=2):
    for i in range(N):
      self.args.append(cl1())
  
  def sort(self):
    self.args = sorted(self.args, 
    key=lambda name: name.name)

  def dup_check(self):
    a_set = set(self.args)
    return (len(self.args) != len(a_set))

  def sign(self):
    cnt=0;
    N = len(self.args)
    i = 0
    while(i < N):
      j = i+1
      while(j < N):
        if ((self.args[i].name)>(self.args[j].name)):
          cnt +=1
        j+=1
      i+=1
    return cnt%2;


z = cl2()
print(z.args)
print(z.sign())
z.sort()
print(z.args)
z.args[0].name='we'
z.args[1].name='we'
print(z.dup_check())
print(z.args)
  # def __eq__(self, other):
  #   return (
  #     self.__class__ == other.__class__ and
  #     self.name == other.name
  #   )
  # def __lt__(self, other):
  #   return (
  #     self.__class__ == other.__class__ and
  #     self.name > other.name
  #   )
  # def __gt__(self, other):
  #   return (
  #     self.__class__ == other.__class__ and
  #     self.name < other.name
  #   )