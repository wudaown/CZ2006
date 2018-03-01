package ss4.Control;

public class TeacherManager {
    private static TeacherManager singleInstance = new TeacherManager();

    private TeacherManager() {

    }
    public static TeacherManager getInstance() {
        return singleInstance;
    }
}
