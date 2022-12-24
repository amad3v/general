fun main() {
    val prefix = "kwriteconfig5 --file \$HOME/.config/kde.org/UserFeedback.org.kde.plasmashell.conf"

    val config =
            """
[Greeter][Wallpaper][org.kde.image][General]
Image=file:///home/shalva/Pictures/lock-screen-wallpaper.jpg

    """.trimIndent()

    var configCommand = StringBuilder()
    var groupCommand = ""

    config.lines().filter { it.isNotEmpty() }.forEach {
        if (it.startsWith("[")) {
            groupCommand = ""
            it.replace("]", "").split("[").filter { it.isNotEmpty() }.forEach { group ->
                groupCommand += "--group \"$group\" "
            }
        } else {
            ("$prefix $groupCommand--key \"" + it.split("=").joinToString("\" \"").plus("\"\n"))
                    .run(configCommand::append)
        }
    }

    print(configCommand)
}
