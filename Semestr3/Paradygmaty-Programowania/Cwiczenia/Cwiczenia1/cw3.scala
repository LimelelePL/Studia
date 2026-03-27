object cw3 extends App {
  def replicate [A] (elem:A, n:Int) : List[A] = {
    if n == 0 then Nil
    else elem :: replicate(elem, n-1) 
  }

  val repl = replicate("fe", 0)
  print(repl.toString)
}
