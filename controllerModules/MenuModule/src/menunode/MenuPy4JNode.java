package menunode;

import py4jmediator.*;
import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Node;
import controlnode.Py4JNode;

public class MenuPy4JNode extends Py4JNode implements MainMenuPresenter.OnMenuPresenterCalled{

	private MenuPy4JNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName) {
		super(dr, dispatchCenter, nodeName);
	}
		
	public MenuPy4JNode(DispatchCenter dispatchCenter, String nodeName){
		this(null, dispatchCenter, nodeName);
	}
	
	@Override
	public void atUnload() {
		
	}

	@Override
	protected void onLoop() {
		
	}

	@Override
	protected void atStart() {
		MainMenuPresenter mainMenuPresenter = Presenter.getInstance().getMainMenuPresenter();
		mainMenuPresenter.setOnMenuPresenterCalled(this);
		mainMenuPresenter.displayMainMenu();
	}

	@Override
	protected void atExit() {
		Presenter.getInstance().getMainMenuPresenter().setOnMenuPresenterCalled(null);
	}

	@Override
	public void onGoToLoader() {
		moveTo("LoaderNode");		
	}

	@Override
	public void onGoToCreator() {
		moveTo("CreatorNode");		
	}

	@Override
	public void onExit() {
		moveTo(null);
		
	}

}
