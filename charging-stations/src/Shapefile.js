import { useEffect } from "react";
import PropTypes from "prop-types";
import { useMap } from "react-leaflet";
import L from "leaflet";
import shp from "shpjs";

function Shapefile({ zipUrl }) {
    const map = useMap()

  useEffect(() => {
    const geo = L.geoJson(
      { features: [] },
      {
        onEachFeature: function popUp(f, l) {
          var out = [];
          if (f.properties) {
            for (var key in f.properties) {
              out.push(key + ": " + f.properties[key]);
            }
            l.bindPopup(out.join("<br />"));
          }
        }
      }
    ).addTo(map);
    console.log("before zip")
    shp("tm.zip").then(function (data) {

        console.log("in zip")
      geo.addData(data);
    });
  }, []);

  return null;
}

Shapefile.propTypes = {
  zipUrl: PropTypes.string.isRequired
};

export default Shapefile;