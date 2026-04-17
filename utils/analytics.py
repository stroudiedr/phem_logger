import streamlit.components.v1 as components


def inject_analytics():
    components.html(
        """
        <script
            data-goatcounter="https://phemlogger.goatcounter.com/count"
            async src="//gc.zgo.at/count.js">
        </script>
        """,
        height=0,
    )
