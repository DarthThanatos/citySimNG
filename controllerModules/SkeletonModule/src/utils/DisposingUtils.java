package utils;


import io.reactivex.disposables.Disposable;

public class DisposingUtils {

    public static void dispose(Disposable trash){
        if(trash != null && !trash.isDisposed()){
            trash.dispose();
        }
    }

}
