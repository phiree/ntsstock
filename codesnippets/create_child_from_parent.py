
class A(object):
  ap1='ap1'
class B(A):
  bp1='bp1'
  def __init__(self):
    self.p2='bb'

if __name__=="__main__":
  a=A(ap1='ap1_')
  print(a.ap1)
  b=B()
  print(b.ap1)
  