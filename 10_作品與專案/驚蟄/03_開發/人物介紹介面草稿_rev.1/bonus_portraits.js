// Accepted bonus art is separate from the automatically generated story gallery.
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
  }]
};
