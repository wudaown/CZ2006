package ss4.Control;

public class FilterManager {
    private static FilterManager singleInstance = new FilterManager();

    private FilterManager() {

    }
    public static FilterManager getInstance() {
        return singleInstance;
    }
}
