import java.util.LinkedList
import scala.collection.mutable.Queue
import scala.compiletime.ops.int
object lab8S extends App {
    
def printAll(elems: Any*): Unit = {
    for (x <- elems ) {
        if (x != null) then 
            println(x.getClass().getSimpleName() + ": " + x)
        else println("uwaga: null!")
    }
}

printAll(1,2,"3", 3.3)
printAll(null, None, Nil,  LinkedList(), Queue[Int]())

def whileloop(cond: Boolean, body:Unit) : Unit = {
    if cond then {
        body
        whileloop (cond, body)
    }
     else ()
}

var count = 0
whileloop(
    count<3,
     {
        print(count)
        count += 1
    }
)

}
