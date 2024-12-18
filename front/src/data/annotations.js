export default {
  text: '李白乘舟将欲行，忽闻岸上踏歌声。jkasndkj anjknjknkjnjknjknjknjk李白乘舟将欲行，忽闻岸上踏歌声。jkasndkj anjknjknkjnjknjknjknjkndkj anjknjknkjnjknjknjkn',
  entities: [
    {
      id: 1,
      start: 0,
      end: 2,
      label: '人物',
      color: { background: '#ffa500', border: '#ff4500', fill: '#ff4500' },
      text: '李白',
    },
    {
      id: 2,
      start: 13,
      end: 14,
      label: '事件',
      color: { background: '#90ee90', border: '#008000', fill: '#008000' },
      text: '歌声',
    },
    {
      id: 3,
      start: 4,
      end: 5,
      label: '人物',
      color: { background: '#ffa500', border: '#ff4500', fill: '#ff4500' },
      text: '将欲',
    },
    {
      id: 4,
      start: 8,
      end: 10,
      label: '事件',
      color: { background: '#90ee90', border: '#008000', fill: '#008000' },
      text: '忽闻岸',
    },
  ],
  relations: [
    { from: 1, to: 2, type: '相关', color: 'red' }, // 蓝色箭头和箭身
    { from: 3, to: 4, type: 'ASD', color: 'blue' }, // 蓝色箭头和箭身
  ],
  enti: [
    {
      label: '人物',
      number: 2,
      disabled: false,
      color: { background: '#ffa500', border: '#ff4500', fill: '#ff4500' },
    },
    {
      label: '事件',
      number: 2,
      disabled: false,
      color: { background: '#90ee90', border: '#008000', fill: '#008000' },
    },
  ],
}
