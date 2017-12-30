package py4jmediator;

import org.json.JSONObject;

public class CreatorPresenter {
	
	private OnCreatorPresenterCalled onCreatorPresenterCalled;
	
	public void setOnCreatorPresenterCalled(OnCreatorPresenterCalled onCreatorPresenterCalled){
		this.onCreatorPresenterCalled = onCreatorPresenterCalled;
	}
	
	public void returnToMenu(){
		if(onCreatorPresenterCalled != null)
			onCreatorPresenterCalled.onReturnToMenu();
	}
	
	public void createDependencies(CreatorData creatorData){
		if(onCreatorPresenterCalled != null)
			onCreatorPresenterCalled.onCreateDependencies(creatorData);
	}
	
	public void displayCreator(){
		Presenter.getInstance().getViewModel().getCreatorViewModel().displayCreator();
	}
	
	public void displayDependenciesGraph(JSONObject jsonGraph){
			Presenter
					.getInstance()
					.getViewModel()
					.getCreatorViewModel()
					.displayDependenciesGraph(jsonGraph);
	}
	
	public void displayMsg(String msg){
		Presenter.getInstance().getViewModel().getCreatorViewModel().displayMsg(msg);
	}
	
	public interface OnCreatorPresenterCalled{
		public void onCreateDependencies(CreatorData creatorData);
		public void onReturnToMenu();
	}
}
