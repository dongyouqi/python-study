<?

namespace php;

interface fly{

}

class Person 
{   
}


class Student extends Person 
{
    
    protected $name = '';

    public function setNameCn($name){
        $this->name = $name;
        
    }

    public function print() {
        echo $this->name;
    }
}

$student = new Student();

$student->setNameCn('齐冬有');
$student->print();




?>