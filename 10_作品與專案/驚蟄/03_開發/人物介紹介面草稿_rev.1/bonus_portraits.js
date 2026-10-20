// Bonus art and review candidates are separate from the automatically generated story gallery.
// A variant may be a head-only PNG, or a viewport crop of an existing source.
// A head variant belongs to its base portrait and does not add a gallery entry.
const bonusPortraitGallery = {
  jingzhe: [{
    name: 'bonus jingzhe school_uniform',
    label: '番外彩蛋・學生制服',
    src: 'assets/bonus/jingzhe_school_uniform_no_hat.png',
    variants: [{
      label: '戴帽差分',
      src: 'assets/bonus/jingzhe_school_uniform_hat_source.png',
      sourceSize: [1024, 1536],
      crop: [360, 12, 290, 282]
    }]
  }],
  hanami: [{
    name: 'bonus hanami modern_school_uniform_candidate_01',
    label: '番外彩蛋・現代學生制服',
    src: 'assets/bonus/hanami_modern_school_uniform_candidate_01.png',
    status: 'adopted_art_and_composition'
  }],
  yumemi: [{
    name: 'bonus yumemi sailor_uniform',
    label: '番外彩蛋・水手服',
    src: 'assets/bonus/yumemi_sailor_uniform.png',
    status: 'adopted_art_and_composition',
    variants: [{
      label: '深紫粗框眼鏡',
      src: 'assets/bonus/yumemi_sailor_uniform_glasses_head.png',
      status: 'adopted_art_and_composition'
    }]
  }],
  jorogumo: [{
    name: 'bonus jorogumo school_doctor_candidate_01',
    label: '番外彩蛋・保健室女醫',
    src: 'assets/bonus/jorogumo_school_doctor_candidate_01.png',
    status: 'adopted_art_and_composition',
    variants: [{
      label: '下半框細邊眼鏡',
      src: 'assets/bonus/jorogumo_school_doctor_lower_half_rim_glasses_head.png',
      status: 'adopted_art_and_composition'
    }]
  }],
  tsuchigumo: [{
    name: 'bonus tsuchigumo chibi_enclosure_candidate_01',
    label: '番外彩蛋・昆蟲箱Q版',
    src: 'assets/bonus/tsuchigumo_chibi_enclosure_candidate_01.png',
    status: 'adopted_art_and_composition'
  }],
  kamikiri: [{
    name: 'bonus kamikiri long_white_tshirt_candidate_01',
    label: '番外彩蛋・擋車長版T恤（候選）',
    src: 'assets/bonus/kamikiri_long_white_tshirt_candidate_01.png',
    status: 'candidate_awaiting_user_review'
  }],
  omukade: [{
    name: 'bonus omukade human_black_knit_brown_skirt_candidate_01',
    label: '番外彩蛋・人形黑毛衣棕長裙（候選）',
    src: 'assets/bonus/omukade_human_black_knit_brown_skirt_candidate_01.png',
    status: 'candidate_awaiting_user_review'
  }]
};
