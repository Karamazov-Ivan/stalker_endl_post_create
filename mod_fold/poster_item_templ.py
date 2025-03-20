def text_post(some_text, cost):
    total = rf""";=================POSTER_{some_text}
[decor_poster{some_text}]:tch_junk
class									= II_ATTCH
kind								    = i_tool
visual									= dynamics\efp_props\prop_poster_vertical_{some_text}.ogf

description								= st_placeable_poster{some_text}_descr
inv_name								= st_placeable_poster{some_text}
inv_name_short							= st_placeable_poster{some_text}
icons_texture							= ui\ui_maid_efp_props
inv_grid_x								= 3
inv_grid_y								= 5
inv_grid_width							= 1
inv_grid_height							= 2
cost									= {cost}
inv_weight								= 0.01

; Функтор для размещения
use2_functor         				    = placeable_furniture.place_item
use2_action_functor  					= placeable_furniture.func_place_item

; WG читабельный функтор
wg_readable                                      = true
use1_functor                                     = western_goods_ui_readable.menu_view
use1_action_functor                              = western_goods_ui_readable.use_item
use1_allow_db                                    = true

placeable_type                          = prop
placeable_section                       = placeable_poster{some_text}

snd_on_take								= paper
repair_part_bonus	 	                = 0.02

[placeable_poster{some_text}]:physic_object
visual									= dynamics\efp_props\prop_poster_vertical_{some_text}.ogf
placeable_type                          = prop
base_rotation                           = 0
script_binding                          = bind_hf_base.init
item_section                            = decor_poster{some_text}
ui_texture                              = ui_decor_poster{some_text}
bounding_box_size                       = 0.570892, 0.747018, 0.017975
bounding_box_origin                     = -0.02095, 0.012679, -0.005057"""

    return total

def text_post_horizont(some_text, cost):
    total = rf""";=================POSTER_{some_text}_horizont
[decor_poster{some_text}]:tch_junk
class									= II_ATTCH
kind								    = i_tool
visual									= dynamics\efp_props\prop_poster_vertical_{some_text}.ogf

description								= st_placeable_poster{some_text}_descr
inv_name								= st_placeable_poster{some_text}
inv_name_short							= st_placeable_poster{some_text}

icons_texture							= ui\ui_decor
inv_grid_x								= 10
inv_grid_y								= 7
inv_grid_width							= 2
inv_grid_height							= 2

cost									= {cost}
inv_weight								= 0.01

; Функтор для размещения
use2_functor         				    = placeable_furniture.place_item
use2_action_functor  					= placeable_furniture.func_place_item

; WG читабельный функтор
wg_readable                                      = true
use1_functor                                     = western_goods_ui_readable.menu_view
use1_action_functor                              = western_goods_ui_readable.use_item
use1_allow_db                                    = true

placeable_type                          = prop
placeable_section                       = placeable_poster{some_text}

[placeable_poster{some_text}]:physic_object
visual									= dynamics\efp_props\prop_poster_vertical_{some_text}.ogf
placeable_type                          = prop
base_rotation                           = 0

script_binding                          = bind_hf_base.init
item_section                            = decor_poster{some_text}

ui_texture                              = ui_decor_poster1

bounding_box_size                        = 1.26404, 0.882494, 0.0004
bounding_box_origin                      = 0, 0.002616, 0"""
    
    return total