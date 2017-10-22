package py4jmediator;

public class TutorialPresenter {
	
	private OnTutorialPresenterCalled onTutorialPresenterCalled;
	
	public void setOnTutorialPresenterCalled(OnTutorialPresenterCalled onTutorialPresenterCalled){
		this.onTutorialPresenterCalled = onTutorialPresenterCalled;
	}
	
	public void returnToMenu(){
		if(onTutorialPresenterCalled != null)
			onTutorialPresenterCalled.onReturnToMenu();
	}

	public void fetchTutorialPage(int pageNr){
		if(onTutorialPresenterCalled != null)
			onTutorialPresenterCalled.onFetchTutorialPage(pageNr);
	}
	
	public void displayTutorial(){
		Presenter.getInstance().getViewModel().getTutorialViewModel().displayTutorial();
	}
	
	public void displayTutorialPage(JSONObject jsonPage){
		Presenter.getInstance().getViewModel().getTutorialViewModel().displayTutorialPage(jsonPage);
	}

	public void displayDependenciesGraph(JSONObject jsonGraph){
		Presenter.getInstance().getViewModel().getTutorialViewModel().displayDependenciesGraph(jsonGraph);
	}
	
	
	public interface OnTutorialPresenterCalled{
		public void onReturnToMenu();
		public void onFetchTutorialPage(int pageNr);
	}
}
