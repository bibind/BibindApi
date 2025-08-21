odoo.define('bibind_portal_projects.burn_chart', function (require) {
    'use strict';

    const fieldRegistry = require('web.field_registry_owl');
    const { Component, onMounted, useRef } = owl;

    class BurnChart extends Component {
        setup() {
            this.canvasRef = useRef('canvas');
            onMounted(() => {
                const value = this.props.value || {};
                const labels = (value.labels || []);
                const data = (value.values || []);
                if (window.Chart) {
                    new Chart(this.canvasRef.el.getContext('2d'), {
                        type: 'line',
                        data: { labels, datasets: [{ label: 'Burn', data }] },
                        options: { responsive: true }
                    });
                }
            });
        }
    }
    BurnChart.template = 'bibind_portal_projects.BurnChart';

    fieldRegistry.add('burn_chart', BurnChart);
});
