package ss4.Control;

public class ParentManager {
    private static ParentManager singleInstance = new ParentManager();

    private ParentManager() {

    }
    public static ParentManager getInstance() {
        return singleInstance;
    }
}
