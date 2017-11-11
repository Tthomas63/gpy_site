<all-user-search>
    <div class="ui input">
        <input id="search-text" type="text" placeholder="Search...">
    </div>
    <div class="ui icon input">
        <button class="ui right floated icon button" type="submit" onclick={search_btn_click}>
            <i class="search icon"></i>
            <p></p>
        </button>
    </div>

    <script>
        var self = this;

        self.search_btn_click = function () {
            var search_text = $('#search-text').val();
            console.log(search_text)
            var search_url = search_user_url + search_text;
            window.location = search_url;
        }
    </script>
</all-user-search>