import { defineStore } from 'pinia'
import { Sensor } from '@/types'

export const useSensorStore = defineStore('sensor', {
  state: () => ({ sensors: [] as Sensor[], loaded: false }),
  getters: {},
  actions: {
    async fetchSensors() {
      if (this.sensors.length > 0) return
      try {
        const { data } = await this.$http.get('/sensors')
        this.sensors = data
        this.loaded = true
      } catch (error) {
        console.error('Error fetching units from DB', error)
      }
    },
    async updateSensor(sensor: Sensor) {
      try {
        const { data } = await this.$http.patch(`/sensors/${sensor.id}`, sensor)
        const index = this.sensors.findIndex((s) => s.id === sensor.id)
        if (index !== -1) {
          this.sensors[index] = data
        }
      } catch (error) {
        console.error('Error updating sensor', error)
      }
    },
    async createSensor(sensor: Sensor) {
      try {
        const { data } = await this.$http.post('/sensors', sensor)
        this.sensors.push(data)
        return data
      } catch (error) {
        console.error('Error creating sensor', error)
      }
    },
    getSensorById(id: string) {
      const sensor = this.sensors.find((sensor) => sensor.id === id)
      if (!sensor) throw new Error(`Processing Level with id ${id} not found`)
      return sensor
    },
  },
})