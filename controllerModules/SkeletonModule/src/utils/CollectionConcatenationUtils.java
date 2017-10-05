package utils;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

public class CollectionConcatenationUtils {

    public static String mapToString(Map<String, Integer> map){
        return map.size() == 0 ? "" : map.entrySet().stream().map( es -> es.getKey() + " -> " + es.getValue() + "\n").reduce((v1, v2) -> v1 + v2).get();
    }

    public static String filteredMapToString(Map<String, Integer> map){
        Set<Map.Entry<String, Integer>> filteredEntries = map.entrySet().stream().filter(e -> e.getValue() > 0).collect(Collectors.toSet());
        return filteredEntries.size() == 0 ? "" : filteredEntries.stream().map( es -> es.getKey() + " -> " + es.getValue() + "\n").reduce((v1, v2) -> v1 + v2).get();
    }


    public static String listToString(List<? extends Object> list){
        return list.size() == 0 ? "" : list.stream().map(Object::toString).reduce((r1, r2) -> r1 + r2).get();

    }
}
