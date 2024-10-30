/** @odoo-module **/
import { registry } from "@web/core/registry";
import { onWillStart,Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class CompareComponent extends Component {
  
  setup() {
    
    super.setup();
    this.orm = useService("orm");
    this.action = useService("action");
    this.user = useService("user");
    this.order_list=useState([])
    this.product_list=useState([])
    this.sale_order_ids=useState([])
    this.grupo=useState([])
    onWillStart(async () => {
                await this.get_data()
                this.grupo = await this.user.hasGroup("purchase.group_purchase_user");
              });
  }

  async get_data(){
      //si no esta definido el contexto se llama al localstorage
      if (this.props.action.context.purchase_order_ids==undefined){
        var ids = localStorage.getItem("domain");//se obtien del localstorage
        this.sale_order_ids= JSON.parse("[" + ids + "]");
      }else{
         //si esta definido el contexto se guarda en el localstorage
        localStorage.setItem("domain", this.props.action.context.purchase_order_ids);
        this.sale_order_ids=this.props.action.context.purchase_order_ids
      }

      const domain = [["order_id", "in", this.sale_order_ids]]; 
      const domain_order = [["id", "in", this.sale_order_ids]]; 
      //se llama a un metodo que para obtener los datos 
      this.state = await this.orm.call("purchase.order.line", "get_data", [
          domain, domain_order
      ]);

      //se guardan los datos en variables generales
      this.state.order_list.forEach(element => {
        this.order_list.push(element)
        
      });
      this.state.product_list.forEach(element => {
        this.product_list.push(element)
        
      });
  }

  //metodo que elimina productos
  btn_delete_record(ev) {
    const product_line_id = parseInt(ev.target.id);
    this.orm.call("purchase.order.line", "delete_record", [
        product_line_id
    ]).then(function (arrays) {
      if ((arrays = true)) {
        location.reload();
      }
    })
  }

  //metodo que confirma la orden
  btn_confirm_order(ev){
    const order_id = parseInt(ev.target.id);
    this.orm.call("purchase.order", "button_confirm", [
      order_id
    ]).then(function (arrays) {
      if ((arrays = true)) {
        location.reload();
      }
    })
  }

  //metodo que visualiza la orden deseada
  view_order(ev) {
    ev.stopPropagation();
    ev.preventDefault();
    const id = parseInt($(ev.target.attributes.value).val(), 10);

    // Verificar si this.grupo está definido y es true
    if (this.grupo) {
        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "purchase.order",
            view_mode: "form",
            res_id: id,
            views: [[false, "form"]],
            target: "main",
        });
    } 
  }

  //metodo que visualiza al proveedor deseado
  view_partner(ev) {
    ev.stopPropagation();
    ev.preventDefault();
    const id = parseInt($(ev.target.attributes.value).val(), 10);

    // Verificar si this.grupo está definido y es true
    if (this.grupo) {
        var options = {
            on_reverse_breadcrumb: self.on_reverse_breadcrumb,
        };
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "res.partner",
            view_mode: "form",
            res_id: id,
            views: [[false, "form"]],
            target: "main",
        });
    } 
  }

  //metodo que confirma la orden
  btn_confirm_orders (ev) {
    var self = this;
    var products = this.product_list;
      var flag = false;
      var orders = [];
      var input_check = false;
      products.forEach((element) => {
        var id = element.id;
        var input = $("input[name*='" + id + "']");
        var checked = false;
        input.each(function (indice, elemento) {
          input_check = true;
          if (elemento.checked == true) {
            checked = true;
            orders.push({
              id: elemento.value,
              product_id: elemento.name,
              accept: true,
            });
          } else {
            orders.push({
              id: elemento.value,
              product_id: elemento.name,
              accept: false,
            });
          }
        });
        if (checked == false) {
          flag = true;
          return true;
        }
      });
      if (flag == false) {
        console.log(orders);
        this.action.doAction({
          context: { orders: orders },
          name: "Confirmar",
          type: "ir.actions.act_window",
          res_model: "confirm.wizard",
          view_mode: "form",
          views: [[false, "form"]],
          target: "new",
      });
      } else {
        if (input_check == true) {
          this.action.doAction({
            type: "ir.actions.client",
            tag: "display_notification",
            params: {
              title: "Error al confirmar cotizaciones",
              message: "No se a seleccionado un producto de la lista",
              type: "danger",
              sticky: false,
            },
          });
        } else {
          this.action.doAction({
            type: "ir.actions.client",
            tag: "display_notification",
            params: {
              title: "No se puede confirmar",
              message: "Ya se han confirmado las cotizaciones",
              type: "warning",
              sticky: false,
            },
          });
        }
      }
    
  }
}
  

CompareComponent.props = {
  order_ids: { type: Object, optional: true },
  defaultTitle: { type: String, optional: true },
  action: { type: Object, optional: true },
  actionId: { type: Number, optional: true },
  className: { type: String, optional: true },
};
  
CompareComponent.template = "compare_template";
registry.category("actions").add("CompareTemplate", CompareComponent);

