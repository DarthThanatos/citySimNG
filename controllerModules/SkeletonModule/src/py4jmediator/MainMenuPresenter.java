package py4jmediator;

public class MainMenuPresenter {
	
	private OnMenuPresenterCalled onMenuPresenterCalled;
	
	public void setOnMenuPresenterCalled(OnMenuPresenterCalled onMenuPresenterCalled){
		this.onMenuPresenterCalled = onMenuPresenterCalled;
	}
	
	public void exitSystem(){
		System.out.println("Exiting...");
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
