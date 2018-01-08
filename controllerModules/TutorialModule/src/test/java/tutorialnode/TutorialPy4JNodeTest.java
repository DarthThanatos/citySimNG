package tutorialnode;

import java.util.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import entities.Building;
import entities.Dweller;
import entities.Resource;

import entities.Entity;
import hintsender.HintSender;
import org.json.JSONObject;
import org.json.JSONArray;

import model.DependenciesRepresenter;
import graph.GraphsHolder;
import graph.BuildingNode;
import graph.DwellerNode;
import graph.ResourceNode;
import graph.GraphNode;

import controlnode.DispatchCenter;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;
import java.lang.reflect.Method;
import java.lang.reflect.Field;
import java.util.logging.Logger;

import java.lang.NoSuchMethodException;
import java.lang.NoSuchFieldException;
import java.lang.IllegalAccessException;
import java.lang.reflect.InvocationTargetException;

public class TutorialPy4JNodeTest{

	private static Logger log = Logger.getLogger(TutorialPy4JNode.class.getName());

	@Mock
    private DispatchCenter dispatchCenter;

    @Mock
    private DependenciesRepresenter dr;

    @Mock
    private GraphsHolder graphsHolder;

    private static final String[] TUTORIAL_INDEX = new String[] {
            "Game - overview",
            "Tutorial - how to use",
            "Map - overview",
            "Map - buildings panel",
            "Map - resources panel",
            "Exchange - overview",
            "Exchange - transactions",
            "Exchange - lottery"
        };
    private List<String> buildingsIndex;
    private List<String> resourcesIndex;
    private List<String> dwellersIndex;
    private ResourceNode resourceNode;
    private BuildingNode buildingNode;
    private DwellerNode dwellerNode;


    private void initIndexes(){
        Resource resource = new Resource();
        Building building = new Building();
        Dweller dweller = new Dweller();

        resourceNode = new ResourceNode(resource);
        buildingNode = new BuildingNode(building);
        dwellerNode = new DwellerNode(dweller);

        dwellersIndex = new ArrayList(Arrays.asList(dwellerNode.getName()));
        buildingsIndex = new ArrayList(Arrays.asList(buildingNode.getName()));
        resourcesIndex = new ArrayList(Arrays.asList(resourceNode.getName()));
    }

    private void mockDispatchCenter(){
    	dispatchCenter = mock(DispatchCenter.class);
    }


    private void mockGraphHolder(){
    	graphsHolder = mock(GraphsHolder.class);
        when(graphsHolder.getBuildingsGraphs()).thenReturn(Arrays.asList(buildingNode));
        when(graphsHolder.getDwellersGraphs()).thenReturn(Arrays.asList(dwellerNode));
        when(graphsHolder.getResourcesGraphs()).thenReturn(Arrays.asList(resourceNode));
        when(graphsHolder.getBuildingNode(buildingNode.getName())).thenReturn(buildingNode);
        when(graphsHolder.getResourceNode(resourceNode.getName())).thenReturn(resourceNode);
        when(graphsHolder.getDwellerNode(dwellerNode.getName())).thenReturn(dwellerNode);
    }

    private void mockDependenciesRepresenter(){
    	dr = mock(DependenciesRepresenter.class);
    	when(dr.getGraphsHolder()).thenReturn(graphsHolder);
    }


    @Before
    public void init(){
    	initIndexes();
        mockDispatchCenter();
        mockGraphHolder();
    	mockDependenciesRepresenter();
    }

    @Test
    public void allIsWellInitialised(){
        assertNotNull(graphsHolder.getBuildingsGraphs());
        assertNotNull(graphsHolder.getDwellersGraphs());
        assertNotNull(graphsHolder.getResourcesGraphs());
        assertNotNull(graphsHolder.getBuildingNode(buildingNode.getName()));
        assertNotNull(graphsHolder.getDwellerNode(dwellerNode.getName()));
        assertNotNull(graphsHolder.getResourceNode(resourceNode.getName()));
        assertNotNull(dr.getGraphsHolder());
    }

    // @Test
    // public void testFetchIndexes() 
    // throws NoSuchMethodException, IllegalAccessException, NoSuchFieldException, InvocationTargetException{
    // 	TutorialPy4JNode tutorial = new TutorialPy4JNode(dr, dispatchCenter, "tutorial");
    //     tutorial.atStart();
    //     Method m = tutorial.getClass().getDeclaredMethod("at");
    //     m.setAccessible(true);
    //     m.invoke(tutorial);

    //     Field f2 = tutorial.getClass().getDeclaredField("TMP_PAGE");
    //     f2.setAccessible(true);
    //     assertNotNull( (String)(f2.get(tutorial)));
    //     assertFalse(("IOException").equals((String)(f2.get(tutorial))));

    //     Field f = tutorial.getClass().getDeclaredField("tutorialIndex");
    //     f.setAccessible(true);
    //     String[] fValue = (String[])(f.get(tutorial));

    //     assertNotNull(fValue);
    //     assertEquals(TUTORIAL_INDEX.length, fValue.length);
    //     for (int i = 0; i < TUTORIAL_INDEX.length; i++) {
    //         assertEquals(TUTORIAL_INDEX[i], fValue[i]);
    //     }
    // }

    @Test
    public void testFetchBuildingsIndex() 
    throws NoSuchMethodException, IllegalAccessException, NoSuchFieldException, InvocationTargetException{
        TutorialPy4JNode tutorial = new TutorialPy4JNode(dr, dispatchCenter, "tutorial");
        Method m = tutorial.getClass().getDeclaredMethod("initGraphsHolder");
        m.setAccessible(true);
        m.invoke(tutorial);

        m = tutorial.getClass().getDeclaredMethod("fetchBuildingsIndex");
        m.setAccessible(true);
        m.invoke(tutorial);

        Field f = tutorial.getClass().getDeclaredField("buildingsIndex");
        f.setAccessible(true);
        List<String> fValue = (List<String>)(f.get(tutorial));

        assertNotNull(fValue);
        assertEquals(buildingsIndex, fValue);
    }

    @Test
    public void testFetchResourcesIndex()
    throws NoSuchMethodException, IllegalAccessException, NoSuchFieldException, InvocationTargetException{
        TutorialPy4JNode tutorial = new TutorialPy4JNode(dr, dispatchCenter, "tutorial");
        Method m = tutorial.getClass().getDeclaredMethod("initGraphsHolder");
        m.setAccessible(true);
        m.invoke(tutorial);

        m = tutorial.getClass().getDeclaredMethod("fetchResourcesIndex");
        m.setAccessible(true);
        m.invoke(tutorial);

        Field f = tutorial.getClass().getDeclaredField("resourcesIndex");
        f.setAccessible(true);
        List<String> fValue = (List<String>)(f.get(tutorial));

        assertNotNull(fValue);
        assertEquals(resourcesIndex, fValue);
    }

    @Test
    public void testFetchDwellersIndex()
    throws NoSuchMethodException, IllegalAccessException, NoSuchFieldException, InvocationTargetException{
        TutorialPy4JNode tutorial = new TutorialPy4JNode(dr, dispatchCenter, "tutorial");
        Method m = tutorial.getClass().getDeclaredMethod("initGraphsHolder");
        m.setAccessible(true);
        m.invoke(tutorial);

        m = tutorial.getClass().getDeclaredMethod("fetchDwellersIndex");
        m.setAccessible(true);
        m.invoke(tutorial);

        Field f = tutorial.getClass().getDeclaredField("dwellersIndex");
        f.setAccessible(true);
        List<String> fValue = (List<String>)(f.get(tutorial));

        assertNotNull(fValue);
        assertEquals(dwellersIndex, fValue);    
    }

    // @Test
    // public void onFetchTutorialPage(){

    // }

    @Test
    public void onFetchBuildingsPage()
    throws NoSuchMethodException, IllegalAccessException, NoSuchFieldException, InvocationTargetException{
        TutorialPy4JNode tutorial = new TutorialPy4JNode(dr, dispatchCenter, "tutorial");
        Method m = tutorial.getClass().getDeclaredMethod("initGraphsHolder");
        m.setAccessible(true);
        m.invoke(tutorial);

        m = tutorial.getClass().getDeclaredMethod("fetchBuildingsIndex");
        m.setAccessible(true);
        m.invoke(tutorial);

        m = tutorial.getClass().getDeclaredMethod("onCorrectTabID", int.class);
        m.setAccessible(true);
        JSONObject result = (JSONObject)(m.invoke(tutorial, 200));
        checkResultCorrectness(result);
    }

    @Test
    public void onFetchDwellersPage()
    throws NoSuchMethodException, IllegalAccessException, NoSuchFieldException, InvocationTargetException{
        TutorialPy4JNode tutorial = new TutorialPy4JNode(dr, dispatchCenter, "tutorial");
        Method m = tutorial.getClass().getDeclaredMethod("initGraphsHolder");
        m.setAccessible(true);
        m.invoke(tutorial);

        m = tutorial.getClass().getDeclaredMethod("fetchDwellersIndex");
        m.setAccessible(true);
        m.invoke(tutorial);

        m = tutorial.getClass().getDeclaredMethod("onCorrectTabID", int.class);
        m.setAccessible(true);
        JSONObject result = (JSONObject)(m.invoke(tutorial, 400));
        checkResultCorrectness(result);
    }

    @Test
    public void onFetchResourcesPage()
    throws NoSuchMethodException, IllegalAccessException, NoSuchFieldException, InvocationTargetException{
        TutorialPy4JNode tutorial = new TutorialPy4JNode(dr, dispatchCenter, "tutorial");
        Method m = tutorial.getClass().getDeclaredMethod("initGraphsHolder");
        m.setAccessible(true);
        m.invoke(tutorial);

        m = tutorial.getClass().getDeclaredMethod("fetchResourcesIndex");
        m.setAccessible(true);
        m.invoke(tutorial);

        m = tutorial.getClass().getDeclaredMethod("onCorrectTabID", int.class);
        m.setAccessible(true);
        JSONObject result = (JSONObject)(m.invoke(tutorial, 300));
        checkResultCorrectness(result);
    }

    private void checkResultCorrectness(JSONObject result){
        assertNotNull(result);
        assertTrue(result.has("Args"));
        assertTrue(result.get("Args") instanceof JSONObject);

        JSONObject args = (JSONObject)(result.get("Args"));

        assertNotNull(args);
        assertTrue(args.has("nr"));
        assertTrue(args.has("sub0"));
        assertTrue(args.has("img"));
        assertTrue(args.has("link"));

        assertTrue(args.get("nr") instanceof Integer);
        assertTrue(args.get("sub0") instanceof JSONArray);
        assertTrue(args.get("img") instanceof String);
        assertTrue(args.get("link") instanceof JSONArray);
    }
}
