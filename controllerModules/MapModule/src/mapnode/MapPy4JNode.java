package mapnode;

import com.google.common.eventbus.Subscribe;
import controlnode.DispatchCenter;
import controlnode.Py4JNode;
import model.DependenciesRepresenter;
import model.TutorialHintEvent;
import py4jmediator.MapPresenter;
import py4jmediator.Presenter;
import py4jmediator.Response;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class MapPy4JNode extends Py4JNode implements MapPresenter.OnMapPresenterCalled {
    public Thread resourcesThread;
    public boolean updateResources = true;

    public Buildings buildings;
    public Dwellers dwellers;
    public Resources resources = null;

    public boolean startNewGame = true;

    private final Lock lock = new ReentrantLock();
    private final Condition viewNotInitialized = lock.newCondition();
    private boolean viewInitialized = false;

    public MapPy4JNode(DependenciesRepresenter dependenciesRepresenter, DispatchCenter dispatchCenter, String nodeName){
        super(dependenciesRepresenter, dispatchCenter, nodeName);
        resources = new Resources(dr);
        buildings = new Buildings(dr);
        dwellers = new Dwellers(dr);
    }

    @Override
    public void atStart(){
        MapPresenter mapPresenter = Presenter.getInstance().getMapPresenter();
        mapPresenter.setOnMapPresenterCalled(this);
        mapPresenter.displayMap();

        waitForViewInit();

        if(startNewGame) {
            lock.lock();
            viewInitialized = false;
            lock.unlock();

            startNewGame = false;
            resources = new Resources(dr);
            buildings = new Buildings(dr);
            dwellers = new Dwellers(dr);
            mapPresenter.init(resources.getResources(), buildings.getAllBuildings(), dr.getTextureAt(0),
                    dr.getTextureAt(1), resources.getActualResourcesValues(), resources.getActualResourcesIncomes());

            waitForViewInit();

        }
        else{
            mapPresenter.resumeGame();
        }

        updateResources = true;
        resourcesThread = new Thread() {
            public void run() {
                while (updateResources) {
                    resources.updateResources();
                    mapPresenter.updateResourcesValues(resources.getActualResourcesValues(),
                            resources.getActualResourcesIncomes());
                    try {
                        Thread.sleep(3000);
                    } catch (Exception e) {
                        System.out.println("Map timer exited while loop");
                    }
                }
                System.out.println("Map timer exited while loop");
            }
        };
        resourcesThread.start();
        registerEvBus();
    }

    @Subscribe
    public void onTutotialHintEvent(TutorialHintEvent tutorialHintEvent){
        //TODO - implementing reaction on tutorialHintEvent receipt
        System.out.println("Map module got hint event with details: " + tutorialHintEvent.getHints());
    }

    @Override
    public void onLoop(){

    }

    private void unregisterEvBus(){
        try{
            dispatchCenter.getEventBus().unregister(this);
        }catch(Exception e) {

        }
    }

    private void registerEvBus(){
        try {
            dispatchCenter.getEventBus().register(this);
        }
        catch(Exception e){

        }

    }

    @Override
    public void atUnload(){
        super.atUnload();
    }

    @Override
    public void atExit(){
        unregisterEvBus();
        resourcesThread.interrupt();
        updateResources = false;
        Presenter.getInstance().getMapPresenter().setOnMapPresenterCalled(null);
    }

    @Override
    public void onGoToMenu(){
        lock.lock();
        viewInitialized = false;
        lock.unlock();
        moveTo("GameMenuNode");
    }


    @Override
    public Response onPlaceBuilding(String buildingName, String buildingId){
        buildings.placeBuilding(buildingName, buildingId, resources, dwellers);
        return new Response(
                resources.getActualResourcesValues(),
                resources.getActualResourcesIncomes(),
                dwellers.getCurrDwellersAmount(),
                dwellers.getCurrDwellersMaxAmount());
    }

    @Override
    public boolean onCheckIfCanAffordOnBuilding(String buildingName){
        return buildings.canAffordOnBuilding(buildingName, resources.getActualResourcesValues());
    }

    @Override
    public Response onDeleteBuilding(String buildingId){
        buildings.deleteBuilding(buildingId, resources, dwellers);
        return new Response(
                resources.getActualResourcesValues(),
                resources.getActualResourcesIncomes(),
                dwellers.getCurrDwellersAmount(),
                dwellers.getCurrDwellersMaxAmount());
    }

    @Override
    public Response onStopProduction(String buildingId){
        buildings.stopProduction(buildingId, resources, dwellers);
        return new Response(
                resources.getActualResourcesValues(),
                resources.getActualResourcesIncomes(),
                dwellers.getCurrDwellersAmount(),
                dwellers.getCurrDwellersMaxAmount(),
                buildings.findBuildingWithId(buildingId).isRunning());
    }

    @Override
    public void onViewInitialized(){
        lock.lock();
        viewInitialized = true;
        viewNotInitialized.signal();
        lock.unlock();
    }

    private void waitForViewInit(){
        lock.lock();
        while(!viewInitialized){
            try{
                viewNotInitialized.await();
            } catch (InterruptedException e){
                System.out.println(e.getMessage());
            }
        }
        lock.unlock();
    }
}
