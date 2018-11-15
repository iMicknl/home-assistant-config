class OVApiCard extends HTMLElement {
  set hass(hass) {

    const entityId = this.config.entity;
    const state = hass.states[entityId];
    const name = this.config.name;

    if (!this.content) {
      const card = document.createElement('ha-card');
      card.header = name;
      this.content = document.createElement('div');
      const style = document.createElement('style');
      style.textContent = `
        table {
          width: 100%;
          padding: 6px 14px;
        }
        td {
          padding: 3px 0px;
        }
        td.shrink {
          white-space:nowrap;
        }
        td.expand {
          width: 99%
        }
        span.line {
          font-weight: bold;
          font-size:0.9em;
          padding:3px 8px 2px 8px;
          color: #fff;
          background-color: #888;
          margin-right:0.7em;
          margin-top:3px;
        }
        span.S-Bahn {
          border-radius:999px;
        }
        span.U-Bahn {
        }
        span.Tram {
          background-color: #ee1c25;
        }
        span.Bus {
          background-color: #005f5f;
        }
        span.U1 {
          background-color: #3c7233;
        }
        span.U2 {
          background-color: #c4022e;
        }
        span.U3 {
          background-color: #ed6720;
        }
        span.U4 {
          background-color: #00ab85;
        }
        span.U5 {
          background-color: #be7b00;
        }
        span.U6 {
          background-color: #0065af;
        }
        span.U7 {
          background-color: #c4022e;
        }
        span.U8 {
          background-color: #ed6720;
        }
        span.S1 {
          background-color: #16c0e9;
        }
        span.S2 {
          background-color: #71bf44;
        }
        span.S3 {
          background-color: #7b107d;
        }
        span.S4 {
          background-color: #ee1c25;
        }
        span.S5 {
          background-color: #ffcc00;
          color: black;
        }
        span.S6 {
          background-color: #008a51;
        }
        span.S7 {
          background-color: #963833;
        }
        span.S8 {
          background-color: black;
          color: #ffcb06;
        }
        span.line47 {
          background-color: #4AA3DF;
        }
        span.line53 {
          background-color: #DC3832;
        }
        `
      card.appendChild(style);
      card.appendChild(this.content);
      this.appendChild(card);
    }

    var tablehtml = `
    <table>
    `
    const departures = state.attributes.departures;

    for (let departure of departures) {
      console.log(departure);
      let icon = departure['TransportTypeIcon'];
      let destinationName50 = departure['DestinationName50'];
      let linePlanningNumber = departure['LinePublicNumber'];
      const product = departure['TransportType'];
      let time = departure['ExpectedDepartureTime'];

      const iconel = document.createElement('ha-icon');
      iconel.setAttribute('icon', icon);
      const iconHTML = iconel.outerHTML;

      tablehtml += `
          <tr>
            <td class="shrink" style="text-align:center;">${iconHTML} <span class="line ${product} line${linePlanningNumber} ${linePlanningNumber}">${linePlanningNumber}</span></td>
            <td class="expand"> ${destinationName50}</td>
            <td class="shrink" style="text-align:right;">${this.getTime(time)}</td>
          </tr>
      `;
    }
    tablehtml += `
    </table>
    `

    this.content.innerHTML = tablehtml
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }

    this.config = config;
  }

  getCardSize() {
    return 1;
  }

  getTime(time) {
    const date = new Date(time);

    var hours = zeroPad(date.getHours())
    var mins = zeroPad(date.getMinutes());
    var secs = zeroPad(date.getSeconds())

    return hours + ':' + mins + ':' + secs;
  }
}

function zeroPad(number) {
  return ('0' + number).substr(-2);
}

customElements.define('ovapi-card', OVApiCard);