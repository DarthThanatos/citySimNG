package py4jmediator;

import java.util.HashMap;

public class GameMenuPresenter {

	private OnGameMenuPresenterCalled onGameMenuPresenterCalled;
	
	public void setOnGameMenuPresenterCalled(OnGameMenuPresenterCalled onGameMenuPresenterCalled){
		this.onGameMenuPresenterCalled = onGameMenuPresenterCalled;
	}
		
	public void goToLoader(){
		if(onGameMenuPresenterCalled != null) {
			onGameMenuPresenterCalled.onGoToLoader();
		}
	}

	public void goToExchange(){
		if(onGameMenuPresenterCalled!=null){
			onGameMenuPresenterCalled.onGoToExchange();
		}
	}

    public void goToNewGame(){
		if(onGameMenuPresenterCalled!=null){
			onGameMenuPresenterCalled.onGoToNewGame();
		}
    }
        

    public void goToTutorial(){
		if(onGameMenuPresenterCalled!=null){
			onGameMenuPresenterCalled.onGoToTutorial();
		}
    }
        
	public void displayGameMenu(){
		Presenter.getInstance().getViewModel().getGameMenuViewModel().displayGameMenu();
	}
	public void animateCurrentPrices(HashMap<String, Integer> currentPrices){
		Presenter.getInstance().getViewModel().getGameMenuViewModel().animateCurrentPrices(currentPrices);
	}

	public interface OnGameMenuPresenterCalled{
		public void onGoToNewGame();
		public void onGoToLoader();
		public void onGoToExchange();
		public void onGoToTutorial();
	}
}
