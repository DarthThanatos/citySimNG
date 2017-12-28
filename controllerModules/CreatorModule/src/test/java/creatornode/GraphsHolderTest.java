package creatornode;

import constants.Consts;
import controlnode.DispatchCenter;
import graph.GraphsHolder;
import model.DependenciesRepresenter;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;

import java.util.HashMap;

import static org.junit.Assert.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class GraphsHolderTest {

    @Mock
    private DispatchCenter dispatchCenter;
    GraphsHolder graphsHolder;

    @Before
    public void setUp() throws Exception {
        dispatchCenter = mock(DispatchCenter.class);
        HashMap<String, DependenciesRepresenter> reprensenters = new HashMap<>();
        when(dispatchCenter.getDispatchData(Consts.LOADER_MODULE, Consts.DEPENDENCIES_REPRESENTERS)).thenReturn(reprensenters);
        new CreatorPy4JNode(dispatchCenter, "Creator",
                "..\\..\\resources\\sysFiles\\defaultDependencies\\");
        DependenciesRepresenter dr = reprensenters.get("Moon");
        assertNotNull(dr);
        graphsHolder = dr.getGraphsHolder();
    }

    @Test
    public void testDwellersDisplayGraph(){
        JSONArray dwellersDispGraph = graphsHolder.displayAllGraphs().getJSONArray(Consts.DWELLERS);
        System.out.println(dwellersDispGraph.toString(4));


        assertEquals(
                "Robotnik",
                dwellersDispGraph
                        .getJSONObject(0)
                        .getString("Name")
        );
        assertEquals(
                "Inwestor",
                dwellersDispGraph
                        .getJSONObject(0)
                        .getJSONArray("Children")
                        .getJSONObject(0)
                        .getString("Name")
        );

        assertEquals(
                "Naukowiec",
                dwellersDispGraph
                        .getJSONObject(0)
                        .getJSONArray("Children")
                        .getJSONObject(0)
                        .getJSONArray("Children")
                        .getJSONObject(0)
                        .getString("Name")
        );
        assertEquals(
                "Xenogenetyk",
                dwellersDispGraph
                        .getJSONObject(0)
                        .getJSONArray("Children")
                        .getJSONObject(0)
                        .getJSONArray("Children")
                        .getJSONObject(0)
                        .getJSONArray("Children")
                        .getJSONObject(0)
                        .getString("Name")
        );
    }

    @Test
    public void testRandomEntityNotNull(){
        for(int i = 0; i < 100; i++) {
            assertNotNull(graphsHolder.getRandomBuilding());
            assertNotNull(graphsHolder.getRandomDweller());
            assertNotNull(graphsHolder.getRandomResource());
        }
    }


    private JSONObject fetchEntityByName(JSONArray entities, String entityName){
        for(int i = 0; i < entities.length(); i++){
            JSONObject potentialHit = entities.getJSONObject(i);
            if (potentialHit.getString("Name").equals(entityName)){
                return potentialHit;
            }
        }
        return null;
    }

    @Test
    public void testBuildingsDisplayGraph(){
        JSONArray buildingsDispGraph = graphsHolder.displayAllGraphs().getJSONArray(Consts.BUILDINGS);
        System.out.println(buildingsDispGraph.toString(4));

        assertNotNull(fetchEntityByName(buildingsDispGraph, "Zrodlo gizmo"));


        assertNotNull(
            fetchEntityByName(
                fetchEntityByName(
                        fetchEntityByName(
                                fetchEntityByName(
                                        buildingsDispGraph,
                                        "Plantacja owocow"
                                ).getJSONArray("Children"),
                                "Wytwornia witamin"
                        ).getJSONArray("Children"),
                        "Browar"
                ).getJSONArray("Children"),
                "Cukiernia"
            )
        );

        assertNotNull(fetchEntityByName(buildingsDispGraph, "Kopalnia gleju"));
        assertNotNull(fetchEntityByName(buildingsDispGraph, "Dormitorium robotnikow"));
        assertNotNull(fetchEntityByName(buildingsDispGraph, "Wytwornia egzoszkieletow"));
        assertNotNull(fetchEntityByName(buildingsDispGraph, "Fabryka energodropsow"));

    }

    @Test
    public void testResourcesDisplayGraph(){
        JSONArray resourcesDispGraph = graphsHolder.displayAllGraphs().getJSONArray(Consts.RESOURCES);
        System.out.println(resourcesDispGraph.toString(4));
        assertNotNull(fetchEntityByName(resourcesDispGraph, "Gizmo"));
        assertNotNull(fetchEntityByName(resourcesDispGraph, "Plastyczny egzoszkielet"));
        assertNotNull(fetchEntityByName(resourcesDispGraph, "Owoce"));
        assertNotNull(
                fetchEntityByName(
                        fetchEntityByName(
                                fetchEntityByName(
                                        fetchEntityByName(
                                                resourcesDispGraph,
                                                "Owoce"
                                        ).getJSONArray("Children"),
                                        "Witaminy"
                                ).getJSONArray("Children"),
                                "Zdrowy likier"
                        ).getJSONArray("Children"),
                        "Alkoholowe desery"
                )
        );
    }

    @Test
    public void testResourcesGraph(){

    }

    @Test
    public void testBuildingsGraph(){

    }

    @Test
    public void testDwellersGraph(){

    }

}