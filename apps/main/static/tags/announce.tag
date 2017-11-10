<announce>
    <div class="ui top attached tabular menu">
        <div class="active item">Announcements</div>
    </div>
    <div class="ui grid bottom attached active stacked raised tab segment">
        <div class="ui row">
            <div align="center" each={annonc in announcements} class="ui four wide column raised card">
                <a href="{announcements_detail_view_url}{annonc.pk}"
                   class="ui small {annonc.fields.announcement_type.fields.color} button">{annonc.fields.title}</a>
                <br>
                <br>
                <div class="ui divider"></div>
                <div>
                    <img style="height: 10%" class="ui tiny center aligned circular image" src={'media/'+
                         annonc.fields.image}>
                </div>
                <br>
                <div class="ui divider"></div>
                <div id="base" class="ui bottom attached tiny inverted text segment"><i>{annonc.fields.description}</i>
                </div>
            </div>
        </div>
    </div>
    <script>
        var self = this;

        var get_api_vars = function () {
            $.get(announce_with_types_api_url, function (data) {
                self.announcements = jQuery.parseJSON(data);
                self.update()
            });
        };
        get_api_vars()
        self.update()

    </script>
</announce>