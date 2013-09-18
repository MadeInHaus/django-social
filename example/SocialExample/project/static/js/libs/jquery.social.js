(function($, document, window, undefined) {
    // Optional, but considered best practice by some
    "use strict";

    var twDefaults = {
        message:'options.message Tweet Text',
        windowName: 'twitter-share-dialog',
        width:626,
        height:260
    },
    pnDefaults = {
        description:'options.description Pinterest Description',
        windowName: 'pinterest-share-dialog',
        width:626,
        height:260,
        href:location.href,
        origin:location.origin,
        shareImg:$("meta[property='og:image']").attr("content")
    },
    fbDefaults = {
        shareurl: location.href,
        windowName: 'facebook-share-dialog',
        width:626,
        height:245
    },
    socialMethodArray = {
        facebook:FacebookShare,
        twitter:TwitterShare,
        pinterest:PinterestShare
    }

    function SocialBase(element, options){
        this.options = options;
        var self = this
        function init(){
            var that = this
            $(element).bind('click', function(){
                onElementClick();
                return false;
            })
        }
        function onElementClick(){
            console.log(this)
            window.open(
                self.options.url, 
                self.options.windowName, 
                'width=' + self.options.width+',height=' + self.options.height
            );
        }
        init()
    }

    function TwitterShare(element, options){
        var opts = $.extend({}, twDefaults, options)
        var socialOptions = {
            url:'https://twitter.com/intent/tweet?'+
                encodeURIComponent(location.href)+
                "&text="+encodeURIComponent(opts.message),
        }
        opts = $.extend(opts, socialOptions)
        new SocialBase(element, opts)
    }

    function PinterestShare(element, options){
        var opts = $.extend({}, pnDefaults, options)
        var href = encodeURIComponent(opts.href)
        var shareImg = encodeURIComponent(opts.shareImg)
        var description = encodeURIComponent(opts.description)
        var socialOptions = {
            url:"http://pinterest.com/pin/create/button/?url="+href+
            "&media="+shareImg+
            "&description="+description,
        }
        opts = $.extend(opts, socialOptions)
        new SocialBase(element, opts)
    }

    function FacebookShare(element, options){
        var opts = $.extend({}, fbDefaults, options)
        var socialOptions = {
            url:'https://www.facebook.com/sharer/sharer.php?u='+
                encodeURIComponent(opts.shareurl)
        }
        opts = $.extend(opts, socialOptions)
        new SocialBase(element, opts)
    }

    for(var item in socialMethodArray){
        //had to wrap this or it would grab the last variable set in the for loop
        (function(item, Share){
            $.fn[item] = function(options){
                this.each(function(){
                    var fnKey = 'plugin_'+item;
                    if (!$.data(this, fnKey)) {
                        $.data(this, fnKey, new Share(this, options));
                    }
                })
            }
        })(item, socialMethodArray[item])
    }

})($, document, window);