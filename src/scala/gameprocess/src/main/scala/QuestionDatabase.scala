case class Question(question: String, alternatives: List[String], correctAnswer: Int)
{
    override def toString() = "Question { question: " + question + ", alternatives: " + alternatives.mkString(", ") + ", correctAnswer: " + correctAnswer + " }"
}

object QuestionDatabase {
   val questions: List[Question] = List(Question("This is a question which has correct alternative 2", List("Incorrect alternative", "Correct alternative", "Incorrect alternative", "Incorrect alternative"), 2))
   
   def getQuestion : Question = 
   {
       questions(0)
   }
}