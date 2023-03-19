odoo.define('shipping_site_location.my_widget', function (require) {
    "use strict";

    var FieldChar = require('web.basic_fields').FieldChar;
    var field_registry = require('web.field_registry');

    var MyWidget = FieldChar.extend({
        // 添加自己的逻辑
        events: _.extend({}, FieldChar.prototype.events, {
            'input': '_onInput'
        }),

        _onInput: function (ev) {
            var self = this;
            var e = new KeyboardEvent("keydown", {
              bubbles: true,
              cancelable: true,
              keyCode: 9  // 9 表示 TAB 键的键码
            });
            setTimeout(function() {
                var inputs = document.getElementsByTagName('input');
                var index = Array.prototype.indexOf.call(inputs, document.activeElement);
                var nextInput = inputs[(index) % inputs.length];
                nextInput.focus();
                console.log(nextInput)
                nextInput.dispatchEvent(e);
            }, 1000);
        },

        // 添加一个初始化方法，以便在小部件创建时创建输入框
        init: function () {
            this._super.apply(this, arguments);
            this.$input = this.$el;
        }
    });

    field_registry.add('my_char_field', MyWidget);

    return MyWidget;
});