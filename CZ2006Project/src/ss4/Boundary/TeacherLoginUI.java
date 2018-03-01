package ss4.Boundary;

import ss4.Control.SchoolManager;
import ss4.Control.TeacherManager;
import ss4.Entity.Teacher;

public class TeacherLoginUI implements LoginUI {
    SchoolManager schoolManager = SchoolManager.getInstance();
    TeacherManager teacherManager = TeacherManager.getInstance();
}
