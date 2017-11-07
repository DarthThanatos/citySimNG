package py4jmediator;

import java.util.logging.Level;
import java.util.logging.Logger;

public class MainMenuPresenter {
	
	private OnMenuPresenterCalled onMenuPresenterCalled;
	private static final Logger logger = Logger.getLogger( MainMenuPresenter.class.getName() );
	
	public void setOnMenuPresenterCalled(OnMenuPresenterCalled onMenuPresenterCalled){
		this.onMenuPresenterCalled = onMenuPresenterCalled;
	}
	
	public void exitSystem(){
		logger.log(Level.INFO, "Exiting... ");
		if(onMenuPresenterCalled != null){
			onMenuPresenterCalled.onExit();
		}
	}
	
	public void goToLoader(){
		if(onMenuPresenterCalled != null) {
			onMenuPresenterCalled.onGoToLoader();
		}
	}
	
	public void goToCreator(){
		if(onMenuPresenterCalled != null) {
			onMenuPresenterCalled.onGoToCreator();
		}
	}
	
	public void displayMainMenu(){
		Presenter.getInstance().getViewModel().getMainMenuViewModel().displayMainMenu();
	}
	
	public interface OnMenuPresenterCalled{
		public void onGoToLoader();
		public void onGoToCreator();
		public void onExit();
	}
	
}
