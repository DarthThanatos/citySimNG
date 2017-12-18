package model;

public class TutorialHintEvent {
    private static int id = 1;
    private String hints;
    private static String MOCK_HINT=  " Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam commodo fermentum orci, in molestie urna varius ut. Ut et augue massa. Donec molestie, dolor quis pulvinar eleifend, ex nisl blandit ligula, vitae auctor orci nunc ac dolor. Praesent ante ex, auctor ac lectus non, euismod dapibus dui. Fusce quis quam vitae neque vulputate pretium. Vivamus erat odio, luctus non euismod in, blandit vulputate leo. Praesent vitae quam ante. Praesent sagittis laoreet pellentesque. In lobortis ut urna et vulputate. Etiam eu ornare odio. Mauris sed condimentum arcu. Vestibulum et nisl a nulla posuere semper a sagittis lectus. Aenean hendrerit purus non nunc cursus, et aliquam ex interdum. Vestibulum mollis felis ac dolor tincidunt, non ultricies felis laoreet.\n" +
            "\n" +
            "Pellentesque rhoncus ante condimentum enim ullamcorper, tincidunt tempor dui porta. Pellentesque commodo ullamcorper mi, sollicitudin elementum urna venenatis non. Proin rutrum odio a tellus venenatis, a luctus purus sodales. Fusce feugiat ligula at augue semper dapibus. Nunc sed nisl eget sem dapibus ullamcorper non quis urna. Maecenas a vehicula nibh, et vestibulum augue. Sed condimentum ex eget sem convallis interdum. Integer vestibulum volutpat diam vel rutrum. Suspendisse potenti. Maecenas libero mi, convallis et convallis non, aliquet id augue. Suspendisse sed facilisis leo. Nam iaculis lectus tempus metus hendrerit, vitae laoreet nisi placerat. Quisque faucibus dui metus, quis interdum metus efficitur eu. Mauris varius sollicitudin velit, quis malesuada tellus consectetur vel. Maecenas quis mollis lacus, at porta mauris. Phasellus vulputate velit vel odio commodo mattis.\n" +
            "\n" +
            "In quis finibus odio, sit amet gravida ex. Donec sagittis auctor felis id facilisis. Vivamus suscipit, ex sit amet varius convallis, libero arcu pretium massa, a volutpat purus libero non diam. Morbi quam leo, efficitur nec dictum ut, bibendum vitae mi. Nullam scelerisque ut ipsum sit amet hendrerit. Ut pharetra tortor at nibh lobortis, at efficitur sapien maximus. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.\n" +
            "\n" +
            "Maecenas mollis dui at blandit tempor. Etiam finibus leo sed ex dignissim laoreet. Donec a viverra tellus. Donec feugiat, elit at lacinia egestas, diam elit ullamcorper libero, nec posuere lorem ex ac nunc. Pellentesque elit lacus, eleifend id imperdiet eu, ullamcorper sit amet metus. Quisque sed aliquet eros. Phasellus fermentum neque non vulputate dapibus.\n" +
            "\n" +
            "Cras molestie gravida neque. Sed faucibus ipsum nec lacus pretium pharetra. Vestibulum quis tristique odio. Cras a enim fringilla, tempor urna et, cursus massa. Morbi id nibh enim. Pellentesque et varius purus. Nunc molestie orci magna, id rutrum lorem cursus quis. Maecenas ac ornare mauris. Nam vel diam in mauris mattis placerat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas ac tortor rutrum, aliquam leo sit amet, venenatis mi. Suspendisse scelerisque gravida laoreet. Fusce maximus, erat in euismod varius, lorem turpis auctor nisl, vel auctor nibh nunc at justo. Nulla eleifend faucibus purus ut convallis.\n" +
            "\n" +
            "Donec cursus consectetur viverra. Donec elementum lacinia elit quis pharetra. Nunc et gravida tortor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Curabitur in ante at odio consectetur scelerisque. Praesent.";
    public TutorialHintEvent(String hints){
        this.hints = id + hints;
        id ++;
    }

    public String getHints() {
        return hints;
    }
}
