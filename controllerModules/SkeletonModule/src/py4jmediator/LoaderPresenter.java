package py4jmediator;

import java.util.Set;

import org.json.JSONObject;

public class LoaderPresenter {
	
	private OnLoaderPresenterCalled onLoaderPresenterCalled;
	
	public void setOnLoaderPresenterCalled(OnLoaderPresenterCalled onLoaderPresenterCalled){
		this.onLoaderPresenterCalled = onLoaderPresenterCalled;
	}
	
	public void goToMainMenu(){
		if(onLoaderPresenterCalled != null) onLoaderPresenterCalled.onGoToMainMenu();
	}
	
	public void goToGameMenu(){
		if(onLoaderPresenterCalled != null) onLoaderPresenterCalled.onGoToGameMenu();
	}
	
	public void onShowGraph(String chosenSet){
		if(onLoaderPresenterCalled != null) onLoaderPresenterCalled.onShowGraph(chosenSet);
	}
	
	public void selectDependenciesGraph(String chosenSet){
		if(onLoaderPresenterCalled != null) onLoaderPresenterCalled.onSelectDependenciesGraph(chosenSet);
	}
	
	public void displayGraph(JSONObject graphDesc){
		Presenter.getInstance().getViewModel().getLoaderViewModel().displayDependenciesGraph(graphDesc);
	}
	
	public void displayPossibleDependenciesSets(Set<String> possibleSets){
		Presenter.getInstance().getViewModel().getLoaderViewModel().displayPossibleDependenciesSets(possibleSets);
	}
	
	public void displayLoader(){
		Presenter.getInstance().getViewModel().getLoaderViewModel().displayLoader();
	}
	
	public interface OnLoaderPresenterCalled{
		public void onGoToMainMenu();
		public void onGoToGameMenu();
		public void onShowGraph(String setChosen);
		public void onSelectDependenciesGraph(String chosenSet);
	}
}
