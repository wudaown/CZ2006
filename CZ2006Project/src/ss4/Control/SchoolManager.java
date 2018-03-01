package ss4.Control;

public class SchoolManager {
    private static SchoolManager singleInstance = new SchoolManager();

    private SchoolManager() {

    }
    public static SchoolManager getInstance() {
        return singleInstance;
    }
}
