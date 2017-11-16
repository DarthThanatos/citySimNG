package exchangenode;

import javax.swing.filechooser.FileSystemView;

public class TestMain {
    public static void main(String ... args) {
        String path = FileSystemView.getFileSystemView().getDefaultDirectory().getPath();
        System.out.println(path);
    }
}
