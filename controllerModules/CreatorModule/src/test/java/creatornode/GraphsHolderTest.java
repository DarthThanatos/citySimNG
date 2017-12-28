package creatornode;

import constants.Consts;
import controlnode.DispatchCenter;
import entities.Dweller;
import graph.*;
import model.DependenciesRepresenter;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;

import java.util.HashMap;
import java.util.List;

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

    private <E extends GraphNode> E fetchEntityNode(List<E> roots, String name){
        for(E root: roots){
            if (root.getName().equals(name)){
                return root;
            }
        }
        return null;

    }

    private BuildingNode fetchBuildingRoot(String name){
        return fetchEntityNode( graphsHolder.getBuildingsGraphs(), name);
    }

    private ResourceNode fetchResourceRoot(String name){
        return fetchEntityNode( graphsHolder.getResourcesGraphs(), name);

    }

    private DwellerNode fetchDwellerRoot(String name){
        return fetchEntityNode(graphsHolder.getDwellersGraphs(), name);
    }

    @Test
    public void testResourcesGraph(){
        assertNotNull(fetchResourceRoot("Owoce"));
        assertNotNull(fetchResourceRoot("Gizmo"));
        assertNotNull(fetchResourceRoot("Plastyczny egzoszkielet"));
    }

    @Test
    public void testBuildingsGraph(){
        assertNotNull(fetchBuildingRoot("Plantacja owocow"));
        assertNotNull(fetchBuildingRoot("Dormitorium robotnikow"));
        assertNotNull(fetchBuildingRoot("Fabryka energodropsow"));
        assertNotNull(fetchBuildingRoot("Wytwornia egzoszkieletow"));
    }

    @Test
    public void testDwellersGraph(){
        DwellerNode dwellerLeaf = graphsHolder.getDwellerNode("Robotnik");
        assertNotNull(dwellerLeaf);
        assertNotNull( dwellerLeaf.getChild("Inwestor").getName());
        assertEquals("Inwestor", dwellerLeaf.getChild("Inwestor").getName());
//        assertEquals("Naukowiec", dwellerLeaf.getPredeccessorName());
//        assertEquals("Naukowiec", ((DwellerNode)dwellerLeaf.getPredecessor()).getDweller().getName());
//        assertEquals("Inwestor", dwellerLeaf.getPredecessor().getPredecessor().getName());
//        assertEquals("Inwestor", dwellerLeaf.getPredecessor().getPredeccessorName());
//        assertEquals("Robotnik", dwellerLeaf.getPredecessor().getPredecessor().getPredecessor().getName());
//        assertEquals("Robotnik", dwellerLeaf.getPredecessor().getPredecessor().getPredeccessorName());
//        assertEquals(dwellerLeaf, dwellerLeaf.getPredecessor().getPredecessor().getPredecessor());
//        assertNotNull(fetchDwellerRoot("Robotnik"));
    }

}