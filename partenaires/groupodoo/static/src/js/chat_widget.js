odoo.define('groupodoo.chat_widget', function (require) {
    'use strict';

    const {Component, useState} = owl;
    const rpc = require('web.rpc');

    class GroupodooChatWidget extends Component {
        setup() {
            this.state = useState({messages: []});
        }

        async sendMessage(text) {
            const resp = await rpc.query({
                route: '/groupodoo/api/chat/send',
                params: {session_uuid: this.props.sessionUuid, message: text},
            });
            if (resp && resp.ok) {
                this.state.messages.push({role: 'user', content: text});
            }
        }
    }
    GroupodooChatWidget.template = 'groupodoo.chat_widget';

    return GroupodooChatWidget;
});
